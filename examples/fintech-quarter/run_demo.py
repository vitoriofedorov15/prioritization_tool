"""Exercise real multipart upload and analysis routes without a server or API key."""
from pathlib import Path
import json
import os
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
# Disable AI before importing the application, irrespective of the caller's shell.
os.environ['GEMINI_API_KEY'] = ''
sys.path.insert(0, str(ROOT / 'backend'))
from fastapi.testclient import TestClient
from main import app


def run():
    sessions = []
    with TestClient(app) as client:
        assert client.get('/api/health').json() == {'status': 'ok'}
        for title, method, files in [
            ('MoSCoW · baseline', 'moscow', {'requirements_file':'moscow.csv','weights_file':'baseline-weights.csv'}),
            ('MoSCoW · risk-first', 'moscow', {'requirements_file':'moscow.csv','weights_file':'risk-first-weights.csv'}),
            ('TOPSIS · equal criteria', 'topsis', {'data_file':'topsis.csv'}),
        ]:
            response = client.post('/api/upload', data={'method':method}, files={k:(v,(HERE/v).read_bytes(),'text/csv') for k,v in files.items()})
            response.raise_for_status()
            sid = response.json()['session_id']
            response = client.post(f'/api/analyze/{method}',json={'session_id':sid})
            response.raise_for_status()
            result = response.json()
            assert result['success'] and len(result['results']) == 12
            ai = client.post('/api/ai/interpret',json={'session_id':sid})
            ai.raise_for_status()
            assert ai.json() == {"summary": None, "ai_available": False}
            sessions.append({'method':method,'method_name':title,'results':result['results'],'conflicts':result['conflicts']})
            print(title)
            for rank,(name,value) in enumerate(sorted(result['results'].items(),key=lambda x:-x[1]['score']),1):
                print(f"  {rank:2}. {name:28} {value['score']:5.1f}")
    (HERE/'results.json').write_text(json.dumps(sessions,ensure_ascii=False,indent=2)+'\n')
    lines=['| Alternative | Baseline | Risk-first | TOPSIS |','|---|---:|---:|---:|']
    for name,_ in sorted(sessions[0]['results'].items(),key=lambda x:-x[1]['score']):
        lines.append('| '+name+' | '+' | '.join(str(s['results'][name]['score']) for s in sessions)+' |')
    (HERE/'ranking.md').write_text('\n'.join(lines)+'\n')
    return sessions

if __name__ == '__main__':
    run()
