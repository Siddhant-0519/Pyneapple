import jpype


def start_jvm():
    jpype.startJVM("-Xmx20480m", classpath=["D:/user_pa1n/VSCode/projects/Pyneapple/notebooks/Pineapple.jar"])

    if jpype.isJVMStarted():
        print("JVM has started successfully")
    else:
        print("JVM failed to start")
