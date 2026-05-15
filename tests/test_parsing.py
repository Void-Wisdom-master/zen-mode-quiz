"""Unit tests for parsing functions in quiz_utils.py"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import functions from quiz_utils module
from quiz_utils import normalize_text, normalize_answer, parse_options_zen


class TestNormalizeText:
    """Test cases for normalize_text function."""
    
    def test_none_input(self):
        assert normalize_text(None) == ""
    
    def test_empty_string(self):
        assert normalize_text("") == ""
    
    def test_whitespace_only(self):
        assert normalize_text("   ") == ""
    
    def test_full_width_colon(self):
        assert normalize_text("问题：答案") == "问题:答案"
    
    def test_full_width_parentheses(self):
        assert normalize_text("（A）选项") == "(A)选项"
    
    def test_full_width_period(self):
        assert normalize_text("A．选项") == "A.选项"
    
    def test_full_width_semicolon(self):
        assert normalize_text("A；选项") == "A;选项"
    
    def test_mixed_characters(self):
        result = normalize_text("问题：（A）选项1．B；选项2")
        assert ":" in result
        assert "(" in result
        assert ")" in result
        assert "." in result
        assert ";" in result


class TestNormalizeAnswer:
    """Test cases for normalize_answer function."""
    
    def test_none_input(self):
        assert normalize_answer(None) == ""
    
    def test_empty_string(self):
        assert normalize_answer("") == ""
    
    def test_true_chinese(self):
        assert normalize_answer("对") == "A"
        assert normalize_answer("正确") == "A"
        assert normalize_answer("是") == "A"
    
    def test_false_chinese(self):
        assert normalize_answer("错") == "B"
        assert normalize_answer("错误") == "B"
        assert normalize_answer("否") == "B"
    
    def test_true_english(self):
        assert normalize_answer("TRUE") == "A"
        assert normalize_answer("true") == "A"
        assert normalize_answer("T") == "A"
        assert normalize_answer("YES") == "A"
        assert normalize_answer("Y") == "A"
    
    def test_false_english(self):
        assert normalize_answer("FALSE") == "B"
        assert normalize_answer("false") == "B"
        assert normalize_answer("F") == "B"
        assert normalize_answer("NO") == "B"
        assert normalize_answer("N") == "B"
    
    def test_symbols(self):
        assert normalize_answer("√") == "A"
        assert normalize_answer("✓") == "A"
        assert normalize_answer("×") == "B"
        assert normalize_answer("✗") == "B"
    
    def test_numeric(self):
        assert normalize_answer("1") == "A"
        assert normalize_answer("0") == "B"
    
    def test_single_choice(self):
        assert normalize_answer("A") == "A"
        assert normalize_answer("B") == "B"
        assert normalize_answer("C") == "C"
    
    def test_multiple_choice(self):
        assert normalize_answer("ABC") == "ABC"
        assert normalize_answer("CBA") == "ABC"  # Sorted
        assert normalize_answer("A,B,C") == "ABC"
        assert normalize_answer("A B C") == "ABC"
    
    def test_whitespace_handling(self):
        assert normalize_answer("  A  ") == "A"
        assert normalize_answer("  ABC  ") == "ABC"


class TestParseOptionsZen:
    """Test cases for parse_options_zen function."""
    
    def test_none_input(self):
        q, opts = parse_options_zen(None)
        assert q == ""
        assert opts == {}
    
    def test_empty_string(self):
        q, opts = parse_options_zen("")
        assert q == ""
        assert opts == {}
    
    def test_pattern1_period_separator(self):
        text = "以下哪项是正确的? A. 选项1 B. 选项2 C. 选项3"
        q, opts = parse_options_zen(text)
        assert q == "以下哪项是正确的?"
        assert "A" in opts
        assert "B" in opts
        assert "C" in opts
    
    def test_pattern1_chinese_separator(self):
        text = "问题内容? A、选项1 B、选项2 C、选项3"
        q, opts = parse_options_zen(text)
        assert q == "问题内容?"
        assert opts.get("A") == "选项1"
        assert opts.get("B") == "选项2"
        assert opts.get("C") == "选项3"
    
    def test_pattern2_parentheses(self):
        text = "题目内容 (A) 选项1 (B) 选项2 (C) 选项3"
        q, opts = parse_options_zen(text)
        assert q == "题目内容"
        assert len(opts) == 3
    
    def test_pattern3_compact(self):
        text = "题目A:选项1B:选项2"
        q, opts = parse_options_zen(text)
        assert q == "题目"
        assert opts.get("A") == "选项1"
        assert opts.get("B") == "选项2"
    
    def test_pattern4_newline(self):
        text = "问题？\nA. 第一个选项\nB. 第二个选项\nC. 第三个选项"
        q, opts = parse_options_zen(text)
        assert "问题" in q
        assert len(opts) >= 2
    
    def test_pattern5_no_delimiter(self):
        text = "下列哪项正确？ A选项一 B选项二 C选项三"
        q, opts = parse_options_zen(text)
        assert "下列哪项正确？" in q
        assert len(opts) >= 2
    
    def test_semicolon_separator(self):
        text = "问题 A;选项1 B;选项2"
        q, opts = parse_options_zen(text)
        assert q == "问题"
        assert len(opts) == 2
    
    def test_no_options(self):
        text = "这是一个没有选项的问题"
        q, opts = parse_options_zen(text)
        assert q == text
        assert opts == {}
    
    def test_only_one_option(self):
        text = "问题 A. 只有一个选项"
        q, opts = parse_options_zen(text)
        # Should not parse when less than 2 options
        assert opts == {} or len(opts) < 2


def run_tests():
    """Run all tests and print results."""
    import traceback
    
    test_classes = [TestNormalizeText, TestNormalizeAnswer, TestParseOptionsZen]
    total_tests = 0
    passed_tests = 0
    failed_tests = []
    
    for test_class in test_classes:
        instance = test_class()
        for method_name in dir(instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    getattr(instance, method_name)()
                    passed_tests += 1
                    print(f"[PASS] {test_class.__name__}.{method_name}")
                except AssertionError as e:
                    failed_tests.append((test_class.__name__, method_name, str(e)))
                    print(f"[FAIL] {test_class.__name__}.{method_name}: {e}")
                except Exception as e:
                    failed_tests.append((test_class.__name__, method_name, traceback.format_exc()))
                    print(f"[ERR] {test_class.__name__}.{method_name}: {e}")
    
    print(f"\n{'='*50}")
    print(f"Results: {passed_tests}/{total_tests} passed")
    
    if failed_tests:
        print(f"\nFailed tests:")
        for cls, method, error in failed_tests:
            print(f"  - {cls}.{method}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(run_tests())
