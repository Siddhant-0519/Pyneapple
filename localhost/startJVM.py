import jpype


def start_jvm():
    jpype.startJVM("-Xmx20480m", classpath=["D:/user_pa1n/VSCode/projects/pyneapple_v2/Pyneapple/pyneapple/pyneapple-0.1.0-SNAPSHOT-jar-with-dependencies.jar"])

    if jpype.isJVMStarted():
        print("JVM has started successfully")
    else:
        print("JVM failed to start")
# D:/user_pa1n/VSCode/projects/pyneapple_v2/Pyneapple/pyneapple/pyneapple-0.1.0-SNAPSHOT-jar-with-dependencies.jar