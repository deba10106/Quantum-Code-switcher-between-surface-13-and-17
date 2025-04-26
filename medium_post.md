# A Hello World Quantum Code Switcher: Bridging Surface-13 and Surface-17 Codes (Example Repo)

*By Debasis Mondal, April 2025*

---

## Introduction

Quantum computing holds the promise of solving problems intractable for classical computers, but it is notoriously susceptible to errors due to decoherence and noise. Quantum error correction (QEC) is essential for realizing reliable quantum computation. Among the most promising QEC schemes are **surface codes**, which offer high thresholds and are well-suited for 2D qubit architectures.

> **Note:** This repository is intended as an example or "hello world" demonstration of quantum code switching between two surface codes. It is not a general-purpose library for the broader goal of a flexible, provider-agnostic quantum error correction code switching toolkit. If there is enough interest from the community, I would love to contribute to and manage such a comprehensive library in the future.

However, not all surface codes are created equal. Different codes, such as Surface-13 and Surface-17, support different sets of logical operations and may be better suited for certain quantum hardware or computational tasks. This motivates the need for a **Quantum Code Switcher**—a tool that can seamlessly convert quantum information between different surface code configurations.

## Motivation

- **Diverse Logical Operations:** Some logical gates are natively supported in one code but not in another. Code switching allows leveraging the strengths of each code during a quantum algorithm.
- **Hardware Compatibility:** Quantum service providers may optimize for different surface code layouts. A code switcher enables interoperability and portability across platforms.
- **Error Mitigation:** Switching codes can help mitigate certain error patterns and optimize for lower logical error rates.

## Project Overview

Our open-source Quantum Code Switcher project provides a robust framework for converting quantum information between Surface-13 and Surface-17 codes. The project is designed to be extensible, well-documented, and test-driven, making it a valuable resource for researchers and practitioners in quantum computing.

### Key Features
- **Bidirectional Conversion:** Seamless conversion between Surface-13 and Surface-17 codes.
- **Logical Operations Support:** Documentation of which logical gates are natively available in each code.
- **Comprehensive Testing:** A unified test suite covering various error types (X, Y, Z), logical states (|0⟩, |1⟩), and conversion scenarios.
- **Open-source and Extensible:** Designed for community collaboration and future expansion to other codes or optimization strategies.

## Technical Highlights

- **Implementation:** Built using [PennyLane](https://pennylane.ai/), a leading library for quantum computing and simulation.
- **Code Conversion Circuit:** The `code_conversion_circuit` function encodes, decodes, and measures quantum states for both Surface-13 and Surface-17 codes, handling error injection and logical state preparation.
- **Logical Operations:** The README details which logical gates (X, Z, Hadamard, etc.) are available in each code, highlighting the practical need for code switching.
- **Testing:** The `test_unified.py` file includes 25+ test cases to ensure reliability across a range of scenarios.

## Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/yourusername/quantum-code-switcher.git
   cd quantum-code-switcher
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the Code Switcher:**
   ```bash
   python code_switcher.py --source surface13 --target surface17 --initial 0
   ```
   See the README for full usage instructions and options.

## GitHub Repository

Find the full project, documentation, and test suite on GitHub:

[https://github.com/yourusername/quantum-code-switcher](https://github.com/yourusername/quantum-code-switcher)

## Future Directions

- **Machine Learning Optimization:** Integrate ML or reinforcement learning to optimize circuit operations and error rates based on service provider characteristics.
- **Support for More Codes:** Expand the switcher to handle additional surface code configurations and logical operations.
- **Community Collaboration:** We welcome contributions, feedback, and collaboration from the quantum computing community.

## Conclusion

The Quantum Code Switcher is a step toward more flexible, robust, and interoperable quantum computing. By enabling seamless transitions between different surface code layouts, we hope to accelerate research and application development in the field.

> Again, this repository is an educational and illustrative example, not a full-fledged general-purpose library. If you are interested in collaborating on a larger, community-driven project for quantum error correction code switching, please reach out or express your interest—I'd be excited to help lead and develop such an initiative!

*Try it out, contribute, and help shape the future of quantum error correction!*
