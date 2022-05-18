# CETONI SiLA 2 Pump SDK
## Installation
Run `pip install .` from the root directory containing the file `setup.py`

## Usage
Run `python -m sila_cetoni_pumps --help` to receive a full list of available options

## Code generation
- generate
  ```console
  $ python -m sila2.code_generator new-package -n syringepump_service -o ./sila_cetoni/pumps/syringepumps/sila ./sila_cetoni/pumps/syringepumps/features*.sila.xml
  $ python -m sila2.code_generator new-package -n contiflowpump_service -o ./sila_cetoni/pumps/contiflowpumps/sila ./sila_cetoni/pumps/contiflowpumps/features*.sila.xml
  ```
- update
  ```console
  $ python -m sila2.code_generator update -d ./sila_cetoni/pumps/syringepumps/sila ./sila_cetoni/pumps/syringepumps/features*.sila.xml
  $ python -m sila2.code_generator update -d ./sila_cetoni/pumps/contiflowpumps/sila ./sila_cetoni/pumps/contiflowpumps/features*.sila.xml
  ```
