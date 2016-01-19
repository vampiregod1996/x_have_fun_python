import os

def xtestwriteconfigfile(config, value=0, sstr="UPDATE_CHANNEL_APP_CONFIG_VERSION"):
    print "step into"
    try:
        lines = open(config, 'r').readlines()
        flen = len(lines)
        for i in range(flen):
            print lines[i]
            if sstr in lines[i]:
                rstr = sstr+"="+value
                lines[i] = rstr
        open(config, 'w').writelines(lines)

    except Exception, e:
        print e


print "end"
