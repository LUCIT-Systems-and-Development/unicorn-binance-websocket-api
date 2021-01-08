---
name: Bug report
about: Create a report to help us improve
title: ''
labels: bug
assignees: oliver-zehentleitner

---

<!--
Before opening a new issue, please ensure:
- YOU HAVE READ THE ISSUE GUIDELINES! -> https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/wiki/Issue-Guidelines
- You search for existing bugs/feature requests
- If related to `UnicornFy` post to https://github.com/oliver-zehentleitner/unicorn-fy/issues
- Remove extraneous template details
- Do not prefix title with type of issue (Feature Request, Bug, etc.) The appropriate labels will be added during triage.
- Do not delete any of the template, fill all of it in; even if you think it doesn't apply to your issue.
- If you fail to follow these simple instructions, we will close the ticket.
- [x] This is a checked box. **Do not leave spaces around the `x`!**
-->

Check this or we will delete your issue. (fill in the checkbox with an X like so: [x])
- [ ] I have searched for other issues with the same problem or similar feature requests. 

#### Select one:
- [ ] Bug
- [ ] Feature Request
- [ ] Technical Help
- [ ] Other

#### Environment
- [ ] Are you using the module on a VPS or other Cloud hosting?
- [ ] Are you using the module on a Raspberry Pi?

#### What kind of internet connection do you have?
```
Include here a description of your internet access like cable, lte and up and download rate.
```

#### Average system load (CPU)
```
Include here the ammount of cpu cores and the average system load.
```

#### Hardware specification 
```
Include here a description of the server hardware.
```

#### Operating System? (include version)
- [ ] macOS
- [ ] Windows
- [ ] Linux (include flavour)

#### Options
- [ ] stream_buffer
- [ ] process_stream_data

#### Which endpoint do you connect?
```
Include here the endpint you are connecting to, like binance.com, binance.com-isolated_margin or binance.org-testnet
```

#### Python Version Requirement
- [ ] I am using Python 3.6.1 or above

#### Exact Python Version?
```
Include here the response of 'python --version' AND 'python3 --version'
```

#### Pip Version?
```
Include here the response of 'python3 -m pip --version' or 'pip3 --version'
```

#### Dependencies
Run `pip list > pip_list.txt` and upload the file.

#### UNICORN Binance WebSocket API Version?
```
Did you upgrade to the latest release version with `pip install unicorn-binance-websocket-api --upgrade`?

Please control what version you are using with this script and post the output: https://github.com/oliver-zehentleitner/unicorn-binance-websocket-api/blob/master/tools/get_used_module_version.py
```

#### Description of your issue
```
Include the contents of the log file here. (REMOVE API_KEY, API_SECRET, LISTEN_KEY!!)
```
