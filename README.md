# Stackstorm Setup

All of the below steps are to be performed from st2-docker repository.

## Run Stackstorm

Add following to `files/st2.user.conf` files for code sharing support between sensors and actions. For reference, check [here](https://github.com/StackStorm/st2-docker)

```conf
[packs]
enable_common_libs = True
```

Run docker-compose up command to start stackstorm:

```bash
export ST2_PACKS_DEV=/path/to/this/repo
docker-compose up -d
```

## Install DiligenceVault Pack

To install DiligenceVault pack:

```bash
docker-compose exec st2client bash
# following commands will be run in bash terminal opened after running above command.
# It should be ran after every update to packs.

cd packs.dev/diligencevault
st2 pack install file:///$PWD

```

Refer [this](https://docs.stackstorm.com/reference/packs.html) if you have any issues.

## Generate API Token

To generate API token to communicate with stackstorm API:

```bash
docker-compose exec st2client st2 apikey create -k -m '{"used_by": "my_application"}'
```

This will output an API token. Copy the token and store it for further usage through code. Refer [here](https://docs.stackstorm.com/authentication.html) for further information.
