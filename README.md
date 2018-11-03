# Phantom

## Server

`./server.py`

Example config file:
```
{
    "wait":
    {
        "any":
        {
            "mode":"wait",
            "cmds":[]
        }
    },
    "default":
    {
        "contestant":
        {
            "mode":"exec",
            "cmds":[]
        },
        "worker":
        {
            "mode":"exec",
            "cmds":[]
        }
    }
}
```

Mode:

```
exec: just execute
wait: execute and wait
```

## Client
