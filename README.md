## RK Manager

RK manager is a simple manager/monitor for the linux kernel. Comes with GUI (From https://github.com/rdbende/Azure-ttk-theme).

### Modules needed

Install all the modules with
`pip install -r requirements.txt`

## What can you do with this tool?

Built with python resources you can:

- Look at the CPU structure and usage information;
- Look at RAM usage;
- Look at the governor and frequency settings.

## Notes

Monitoring takes place via the main cluster (policy0). On multi-cluster linux devices with different settings, the information displayed is not reliable.
