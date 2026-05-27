import importlib.util
import os

_BASE = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..", "prioritization_tool", "logic")
)


def _load(name: str, rel_path: str):
    full = os.path.join(_BASE, rel_path)
    spec = importlib.util.spec_from_file_location(name, full)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_moscow_mod = _load("moscow", "MoSCoW/moscow.py")
_parser_mod = _load("moscow_parser", "MoSCoW/parser.py")
_topsis_mod = _load("topsis", "TOPSIS/topsis.py")
_kano_mod = _load("kano", "Kano/kano.py")
_fahp_mod = _load("fuzzy_ahp", "fuzzy_ahp.py")
_ftopsis_mod = _load("fuzzy_topsis", "fuzzy_topsis.py")
_fdelphi_mod = _load("fuzzy_delphi", "fuzzy_delphi.py")
_itopsis_mod = _load("intuitionistic_topsis", "intuitionistic_topsis.py")

moscow_calculate = _moscow_mod.calculate
load_requirements = _parser_mod.load_requirements
load_weights = _parser_mod.load_weights
process_topsis = _topsis_mod.process_topsis
process_kano_csv = _kano_mod.process_kano_csv
process_fuzzy_ahp_type1 = _fahp_mod.process_fuzzy_ahp_type1
process_fuzzy_ahp_type2 = _fahp_mod.process_fuzzy_ahp_type2
calculate_fuzzy_topsis = _ftopsis_mod.calculate_fuzzy_topsis
process_fuzzy_delphi = _fdelphi_mod.process_fuzzy_delphi
process_delphi_ifs = _fdelphi_mod.process_delphi_ifs
calculate_ifs_topsis = _itopsis_mod.calculate_ifs_topsis
