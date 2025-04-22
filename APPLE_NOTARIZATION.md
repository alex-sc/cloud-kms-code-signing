# Apple Code Signing And Notarization

## Summary
Apple Application code signing and notarization consists of two and a half steps:
- Code Signing `codesign --deep --force ...`. This is an almost offline process (besides timestamping) requiring your code signing certificate. Completes in seconds
- Notarization `xcrun notarytool submit ...`. This is an online process when your code is sent to Apple servers and may take seconds to hours
- (optional) Notarization stapling `xcrun stapler staple`. Attaches notarization output to the binary. Not necessary for online verification, but recommended. Doesn't require access to the dev account used for signing/notarization 


## Troubleshooting
Notarization might take a significant amount of time occasionally/for new accounts/apps.

You might want to set time limit for the `xcrun notarytool submit` command:
- `brew install coreutils`
- `timeout 300s xcrun notarytool submit "notarization.zip" --keychain-profile "notarytool-profile" --wait`
- Make sure to zip and save your .app as runner artifact prior to submission
- Now if the notarization times out, you have two options:
- 1. Produce DMG and submit it for notarization. Both APP and DMG won't be stapled (but notarized eventually), so users w/o internet won't be able to verify the notarization offline
- 2. Take the APP submitted for notarization, async wait for the notarization request to complete
    - Staple the APP manually (doesn't require Developer Account access), see commands below
    - Produce DMG and submit for notarization
    - Staple the DMG manually (doesn't require Developer Account access)
### Step by step:
- Download the .zip and extract it
- Make sure notarization has completed `spctl --assess --type execute --verbose MyApp.app`: `MyApp.app: accepted`


## Useful commands
### Signature
```shell
codesign --verify --deep --strict --verbose=2 MyApp.app
```
Signed app output
```shell
MyApp.app: valid on disk
MyApp.app: satisfies its Designated Requirement
```
### Notarization
Show history/status
```shell
xcrun notarytool history ...
Successfully received submission history.
  history
    --------------------------------------------------
    createdDate: 2025-04-22T05:50:39.230Z
    id: a5fc0fe2-1d76-47a5-a1f8-123456789012
    name: notarization.zip
    status: In Progress
    --------------------------------------------------
    createdDate: 2025-04-21T19:22:34.560Z
    id: c25e9ae5-72c9-4cc4-845d-123456789012
    name: notarization.zip
    status: Accepted
    --------------------------------------------------
    createdDate: 2025-04-21T13:01:34.642Z
    id: a26f4dd9-1a6f-488f-9af5-123456789012
    name: notarization.zip
    status: Invalid
```
Show individual submission status
```shell
xcrun notarytool log a26f4dd9-1a6f-488f-9af5-123456789012

{
  "logFormatVersion": 1,
  "jobId": "a26f4dd9-1a6f-488f-9af5-123456789012",
  "status": "Invalid",
  "statusSummary": "Archive contains critical validation errors",
  "statusCode": 4000,
  "archiveFilename": "notarization.zip",
...
}
```
Check the app
```shell
spctl --assess --type execute --verbose MyApp.app
```
Output for stapled app
```shell
MyApp.app: accepted
source=Notarized Developer ID
```
### Stapling
Check
```shell
xcrun stapler validate MyApp.app
```
Stapled app output
```shell
The validate action worked!
```
Non-stapled app output
```shell
MyApp.app does not have a ticket stapled to it.
```
Staple already notarized app
```shell
xcrun stapler staple MyApp.app
```
Output
```shell
The staple and validate action worked!
```