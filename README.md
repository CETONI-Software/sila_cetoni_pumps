# CETONI SiLA 2 Pump SDK
## Installation
Run `pip install .` from the root directory containing the file `setup.py`

## Usage
Run `python -m sila_cetoni_pumps --help` to receive a full list of available options

## Code generation
```console
$ python -m sila2.code_generator new-package -n syringepump_service -o ./sila_cetoni_pumps/syringepumps/sila ../../features/de/cetoni/pumps/syringepumps/*.sila.xml
$ python -m sila2.code_generator new-package -n contiflowpump_service -o ./sila_cetoni_pumps/contiflowpumps/sila ../../features/de/cetoni/pumps/contiflowpumps/*.sila.xml
```
