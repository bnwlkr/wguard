# wguard
Easily Block Websites on macOS 🚧

## Installation 

To install wguard, run:

```
brew tap bnwlkr/wguard
brew install wguard
```


## Usage

### Block sites

```
sudo wguard -b yahoo.com youtube.com
```

### Unblock sites

```
sudo wguard -u yahoo.com youtube.com
```

### List Blocked Sites


```
wguard -l
```

*Note: wguard automatically handles blocking/unblocking the www subdomain*
