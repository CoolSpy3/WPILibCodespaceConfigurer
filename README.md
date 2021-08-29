# WPILibCodespaceConfigurer
This program configures one or more GitHub repositories to add [`Codespaces`](https://github.com/features/codespaces) configuration files to create an enviornment similar to that which is installed by [`WPILib`](https://github.com/wpilibsuite/allwpilib).
To use it, simply run `python configure.py [repos]` where each repo is specified as `<user>/<repo>` (ex. `python configure.py DeepBlueRobotics/RobotCode2021 DeepBlueRobotics/lib199`).
Alternatively, the `-u` option can be used to specify the same user for all repos (ex. `python configure.py -u DeepBlueRobotics RobotCode2021 lib199`)
