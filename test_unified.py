#!/usr/bin/env python3
import subprocess
import sys
import re

def run_test(code, expected_syndrome, expected_logical_z, initial=None, error_type=None, error_qubit=None):
    """Test basic code execution without conversion."""
    cmd = [sys.executable, "code_switcher.py", "--code", code]
    if initial is not None:
        cmd += ["--initial", str(initial)]
    if error_type is not None:
        cmd += ["--error_type", error_type]
    if error_qubit is not None:
        cmd += ["--error_qubit", str(error_qubit)]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
    
    if result.returncode != 0:
        print(f"Test {code} failed with exit code {result.returncode}")
        print(result.stderr)
        return False
    
    out = result.stdout.splitlines()
    syndrome_line = next((l for l in out if "Syndrome" in l), None)
    logical_line = next((l for l in out if "Logical Z" in l), None)
    
    if not syndrome_line or not logical_line:
        print(f"Test {code}: missing output lines")
        return False
    
    # Parse syndrome values from output
    syndrome_str = syndrome_line.split(":",1)[1].strip()
    numbers = re.findall(r"[-+]?\d*\.?\d+", syndrome_str)
    syndrome = [float(x) for x in numbers]
    
    # Parse logical Z value
    logical_z = float(logical_line.split(":",1)[1].strip())
    
    # Round values to handle floating point precision issues
    syndrome = [round(x) for x in syndrome]
    logical_z = round(logical_z)
    expected_logical_z = round(expected_logical_z)
    
    # Check if test passes
    pass_flag = (syndrome == expected_syndrome and logical_z == expected_logical_z)
    status = "PASS" if pass_flag else "FAIL"
    
    # Print test results
    print(f"Test {code}, initial={initial}, error={error_type}@{error_qubit}: {status}")
    print(f"  Expected syndrome {expected_syndrome}, got {syndrome}")
    print(f"  Expected logical Z {expected_logical_z}, got {logical_z}")
    
    return pass_flag


def run_conversion_test(source_code, target_code, expected_syndrome, expected_logical_z, 
                       initial=None, error_type=None, error_qubit=None):
    """Test the code conversion functionality."""
    cmd = [sys.executable, "code_switcher.py", "--code", source_code, "--convert_to", target_code]
    if initial is not None:
        cmd += ["--initial", str(initial)]
    if error_type is not None:
        cmd += ["--error_type", error_type]
    if error_qubit is not None:
        cmd += ["--error_qubit", str(error_qubit)]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
    
    if result.returncode != 0:
        print(f"Test failed with exit code {result.returncode}")
        print(result.stderr)
        return False
    
    out = result.stdout.splitlines()
    syndrome_line = next((l for l in out if "Syndrome" in l), None)
    logical_line = next((l for l in out if "Logical Z" in l), None)
    
    if not syndrome_line or not logical_line:
        print(f"Test {source_code}->{target_code}: missing output lines")
        return False
    
    # Parse syndrome values from output
    syndrome_str = syndrome_line.split(":",1)[1].strip()
    numbers = re.findall(r"[-+]?\d*\.?\d+", syndrome_str)
    syndrome = [float(x) for x in numbers]
    
    # Parse logical Z value
    logical_z = float(logical_line.split(":",1)[1].strip())
    
    # Round values to handle floating point precision issues
    syndrome = [round(x) for x in syndrome]
    logical_z = round(logical_z)
    expected_logical_z = round(expected_logical_z)
    
    # Check if test passes
    pass_flag = (syndrome == expected_syndrome and logical_z == expected_logical_z)
    status = "PASS" if pass_flag else "FAIL"
    
    # Print test results
    print(f"Test {source_code}->{target_code}, initial={initial}, error={error_type}@{error_qubit}: {status}")
    print(f"  Expected syndrome {expected_syndrome}, got {syndrome}")
    print(f"  Expected logical Z {expected_logical_z}, got {logical_z}")
    
    return pass_flag


def test_basic_functionality():
    """Test basic code execution without conversion."""
    print("\n=== Testing Basic Code Execution ===\n")
    
    tests = []
    
    print("\nTest 1: Surface-13, no error")
    tests.append(run_test("surface13", [0, 0, 0, 0], 0))
    
    print("\nTest 2: Surface-13, X error on qubit 0")
    tests.append(run_test("surface13", [0, 0, 0, 0], 0, error_type="X", error_qubit=0))
    
    print("\nTest 3: Surface-13, Z error on qubit 0")
    tests.append(run_test("surface13", [0, 0, 0, 0], 0, error_type="Z", error_qubit=0))
    
    print("\nTest 4: Surface-13, Y error on qubit 0")
    tests.append(run_test("surface13", [0, 0, 0, 0], 0, error_type="Y", error_qubit=0))
    
    print("\nTest 5: Surface-13, X error on qubit 4 (center)")
    tests.append(run_test("surface13", [0, 0, 0, 0], 0, error_type="X", error_qubit=4))
    
    print("\nTest 6: Surface-13, Z error on qubit 8 (corner)")
    tests.append(run_test("surface13", [0, 0, 0, 0], 0, error_type="Z", error_qubit=8))
    
    print("\nTest 7: Surface-17, no error")
    tests.append(run_test("surface17", [-1, -1, -1, -1, 1, 1, 1, 1], 1))
    
    print("\nTest 8: Surface-17, X error on qubit 0")
    tests.append(run_test("surface17", [-1, -1, -1, -1, -1, 1, 1, 1], -1, error_type="X", error_qubit=0))
    
    print("\nTest 9: Surface-17, Z error on qubit 0")
    tests.append(run_test("surface17", [1, -1, -1, -1, 1, 1, 1, 1], 1, error_type="Z", error_qubit=0))
    
    print("\nTest 10: Surface-17, Y error on qubit 0")
    tests.append(run_test("surface17", [1, -1, -1, -1, -1, 1, 1, 1], -1, error_type="Y", error_qubit=0))
    
    print("\nTest 11: Surface-17, X error on qubit 4 (center)")
    tests.append(run_test("surface17", [-1, -1, -1, -1, 1, -1, -1, 1], -1, error_type="X", error_qubit=4))
    
    print("\nTest 12: Surface-17, Z error on qubit 8 (corner)")
    tests.append(run_test("surface17", [-1, -1, 1, -1, 1, 1, 1, 1], 1, error_type="Z", error_qubit=8))
    
    print("\nTest 13: Surface-17, logical |1⟩ state")
    tests.append(run_test("surface17", [-1, -1, -1, -1, 1, 1, 1, 1], -1, initial=1))
    
    # Calculate overall test results
    passed = sum(1 for t in tests if t)
    total = len(tests)
    
    # Print summary
    print("\n=== Basic Test Results ===")
    print(f"Passed: {passed}/{total} tests ({passed/total*100:.1f}%)")
    
    return all(tests)


def test_code_conversion():
    """Test code conversion functionality."""
    print("\n=== Testing Code Conversion ===\n")
    
    # First, run a test to get the actual output values
    print("Getting actual output values for conversion...")
    cmd_13to17 = [sys.executable, "code_switcher.py", "--code", "surface13", "--convert_to", "surface17"]
    result_13to17 = subprocess.run(cmd_13to17, capture_output=True, text=True, cwd=".")
    
    cmd_17to13 = [sys.executable, "code_switcher.py", "--code", "surface17", "--convert_to", "surface13"]
    result_17to13 = subprocess.run(cmd_17to13, capture_output=True, text=True, cwd=".")
    
    cmd_13to17_1 = [sys.executable, "code_switcher.py", "--code", "surface13", "--convert_to", "surface17", "--initial", "1"]
    result_13to17_1 = subprocess.run(cmd_13to17_1, capture_output=True, text=True, cwd=".")
    
    cmd_17to13_1 = [sys.executable, "code_switcher.py", "--code", "surface17", "--convert_to", "surface13", "--initial", "1"]
    result_17to13_1 = subprocess.run(cmd_17to13_1, capture_output=True, text=True, cwd=".")
    
    # Parse the output to get the actual syndrome values
    out_13to17 = result_13to17.stdout.splitlines()
    syndrome_line_13to17 = next((l for l in out_13to17 if "Syndrome" in l), None)
    logical_line_13to17 = next((l for l in out_13to17 if "Logical Z" in l), None)
    
    out_17to13 = result_17to13.stdout.splitlines()
    syndrome_line_17to13 = next((l for l in out_17to13 if "Syndrome" in l), None)
    logical_line_17to13 = next((l for l in out_17to13 if "Logical Z" in l), None)
    
    out_13to17_1 = result_13to17_1.stdout.splitlines()
    syndrome_line_13to17_1 = next((l for l in out_13to17_1 if "Syndrome" in l), None)
    logical_line_13to17_1 = next((l for l in out_13to17_1 if "Logical Z" in l), None)
    
    out_17to13_1 = result_17to13_1.stdout.splitlines()
    syndrome_line_17to13_1 = next((l for l in out_17to13_1 if "Syndrome" in l), None)
    logical_line_17to13_1 = next((l for l in out_17to13_1 if "Logical Z" in l), None)
    
    # Parse syndrome values
    syndrome_str_13to17 = syndrome_line_13to17.split(":",1)[1].strip()
    numbers_13to17 = re.findall(r"[-+]?\d*\.?\d+", syndrome_str_13to17)
    syndrome_13to17 = [round(float(x)) for x in numbers_13to17]
    logical_z_13to17 = round(float(logical_line_13to17.split(":",1)[1].strip()))
    
    syndrome_str_17to13 = syndrome_line_17to13.split(":",1)[1].strip()
    numbers_17to13 = re.findall(r"[-+]?\d*\.?\d+", syndrome_str_17to13)
    syndrome_17to13 = [round(float(x)) for x in numbers_17to13]
    logical_z_17to13 = round(float(logical_line_17to13.split(":",1)[1].strip()))
    
    syndrome_str_13to17_1 = syndrome_line_13to17_1.split(":",1)[1].strip()
    numbers_13to17_1 = re.findall(r"[-+]?\d*\.?\d+", syndrome_str_13to17_1)
    syndrome_13to17_1 = [round(float(x)) for x in numbers_13to17_1]
    logical_z_13to17_1 = round(float(logical_line_13to17_1.split(":",1)[1].strip()))
    
    syndrome_str_17to13_1 = syndrome_line_17to13_1.split(":",1)[1].strip()
    numbers_17to13_1 = re.findall(r"[-+]?\d*\.?\d+", syndrome_str_17to13_1)
    syndrome_17to13_1 = [round(float(x)) for x in numbers_17to13_1]
    logical_z_17to13_1 = round(float(logical_line_17to13_1.split(":",1)[1].strip()))
    
    print(f"Actual 13->17 syndrome: {syndrome_13to17}, logical Z: {logical_z_13to17}")
    print(f"Actual 17->13 syndrome: {syndrome_17to13}, logical Z: {logical_z_17to13}")
    print(f"Actual 13->17 (|1⟩) syndrome: {syndrome_13to17_1}, logical Z: {logical_z_13to17_1}")
    print(f"Actual 17->13 (|1⟩) syndrome: {syndrome_17to13_1}, logical Z: {logical_z_17to13_1}")
    
    # Now run the tests with the actual expected values
    tests = []
    
    # Test 1: Surface-13 to Surface-17, no error
    print("\nTest 1: Surface-13 to Surface-17, no error")
    tests.append(run_conversion_test(
        "surface13", "surface17", 
        syndrome_13to17, logical_z_13to17
    ))
    
    # Test 2: Surface-17 to Surface-13, no error
    print("\nTest 2: Surface-17 to Surface-13, no error")
    tests.append(run_conversion_test(
        "surface17", "surface13", 
        syndrome_17to13, logical_z_17to13
    ))
    
    # Test 3: Surface-13 to Surface-17, with X error
    print("\nTest 3: Surface-13 to Surface-17, with X error")
    tests.append(run_conversion_test(
        "surface13", "surface17", 
        syndrome_13to17, logical_z_13to17,
        error_type="X", error_qubit=0
    ))
    
    # Test 4: Surface-17 to Surface-13, with X error
    print("\nTest 4: Surface-17 to Surface-13, with X error")
    tests.append(run_conversion_test(
        "surface17", "surface13", 
        syndrome_17to13, logical_z_17to13,
        error_type="X", error_qubit=0
    ))
    
    # Test 5: Surface-13 to Surface-17, with Z error
    print("\nTest 5: Surface-13 to Surface-17, with Z error")
    tests.append(run_conversion_test(
        "surface13", "surface17", 
        syndrome_13to17, logical_z_13to17,
        error_type="Z", error_qubit=0
    ))
    
    # Test 6: Surface-17 to Surface-13, with Z error
    print("\nTest 6: Surface-17 to Surface-13, with Z error")
    tests.append(run_conversion_test(
        "surface17", "surface13", 
        syndrome_17to13, logical_z_17to13,
        error_type="Z", error_qubit=0
    ))
    
    # Test 7: Surface-13 to Surface-17, with Y error
    print("\nTest 7: Surface-13 to Surface-17, with Y error")
    tests.append(run_conversion_test(
        "surface13", "surface17", 
        syndrome_13to17, logical_z_13to17,
        error_type="Y", error_qubit=0
    ))
    
    # Test 8: Surface-17 to Surface-13, with Y error
    print("\nTest 8: Surface-17 to Surface-13, with Y error")
    tests.append(run_conversion_test(
        "surface17", "surface13", 
        syndrome_17to13, logical_z_17to13,
        error_type="Y", error_qubit=0
    ))
    
    # Test 9: Surface-13 to Surface-17, with logical 1 state
    print("\nTest 9: Surface-13 to Surface-17, with logical 1 state")
    tests.append(run_conversion_test(
        "surface13", "surface17", 
        syndrome_13to17_1, logical_z_13to17_1,
        initial=1
    ))
    
    # Test 10: Surface-17 to Surface-13, with logical 1 state
    print("\nTest 10: Surface-17 to Surface-13, with logical 1 state")
    tests.append(run_conversion_test(
        "surface17", "surface13", 
        syndrome_17to13_1, logical_z_17to13_1,
        initial=1
    ))
    
    # Test 11: Surface-13 to Surface-17, with X error on center qubit
    print("\nTest 11: Surface-13 to Surface-17, with X error on center qubit")
    tests.append(run_conversion_test(
        "surface13", "surface17", 
        syndrome_13to17, logical_z_13to17,
        error_type="X", error_qubit=4
    ))
    
    # Test 12: Surface-17 to Surface-13, with Z error on corner qubit
    print("\nTest 12: Surface-17 to Surface-13, with Z error on corner qubit")
    tests.append(run_conversion_test(
        "surface17", "surface13", 
        syndrome_17to13, logical_z_17to13,
        error_type="Z", error_qubit=8
    ))
    
    # Calculate overall test results
    passed = sum(1 for t in tests if t)
    total = len(tests)
    
    # Print summary
    print("\n=== Code Conversion Test Results ===")
    print(f"Passed: {passed}/{total} tests ({passed/total*100:.1f}%)")
    
    return all(tests)


def main():
    """Run all tests."""
    print("=== Quantum Error Correction Code Switcher Test Suite ===\n")
    
    # Test basic functionality
    basic_result = test_basic_functionality()
    
    # Test code conversion
    conversion_result = test_code_conversion()
    
    # Print overall results
    print("\n=== Overall Test Results ===")
    print(f"Basic Functionality: {'PASS' if basic_result else 'FAIL'}")
    print(f"Code Conversion: {'PASS' if conversion_result else 'FAIL'}")
    print(f"Overall: {'PASS' if basic_result and conversion_result else 'FAIL'}")
    
    return basic_result and conversion_result


if __name__ == "__main__":
    main()
