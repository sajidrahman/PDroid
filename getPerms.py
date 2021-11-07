import glob, os, subprocess, androguard.misc

out = open("permsOutput.csv", "w")

# Set directory to wherever the APKs are stored
APKsDIR = "/home/blas/pdroid/"

# Takes inventory of the APKs in the directory
apksList = []
os.chdir(APKsDIR)
for apk in glob.glob("*.apk"):
    #print(apk)
    newapk = apk.replace(' ', '')
    #print(newapk)
    if not apk == newapk:
        tmp = "mv " + apk.replace(' ', '\ ') + " " + newapk
        os.system(tmp)
    apksList.append(newapk)

print(apksList)

# Go through each APK in the list and run PDroid
for apk in apksList:
    mv2Dir = "mv " + apk + " PDroid"
    os.system(mv2Dir)
    apkName = "PDroid/" + apk
    cmd = "python3 cli.py --apk " + apk #apkName
    #print(cmd)
    newDir = os.path.join(APKsDIR, "PDroid")
    os.chdir(newDir)
    os.system(cmd)

    # Get the permissions from the APKs manifest file
    print("Manifest Perms")
    app_decompiled, _, dx = androguard.misc.AnalyzeAPK(apk) #apkName)
    app_perm_list = app_decompiled.get_permissions()
    print(app_perm_list)

    # Get the permissions from the PDroid result directory
    print("PDroid Perms")
    pDir = ""
    for f in os.listdir("."):
        print("Here is f: " + f)
        if os.path.isdir(f) and f != "metadata" and f != "pdroid" and f != ".git":
            print("Located this thing: " + f)
            newname = f.replace(' ', '')
            tmp = "mv " + f.replace(' ', '\ ') + " " + newname
            os.system(tmp)
            pDir = newname
    pdroidPerms = 'cat ' + pDir + '/* | grep -Eo "\<android.permission.*[A-Z]\>" | sort -t: -u -k1,1'
    s = subprocess.Popen([pdroidPerms], shell=True, stdout=subprocess.PIPE).stdout
    pPerm = s.read().decode("utf-8").split('\n')[:-1]
    print(pPerm)
    
    # Permissions post-processing to remove weird results
    remove = False
    for j in pPerm:
        for i in j:
            if not i.isalpha() and i != '.' and i != '_':
                print("Gonna delete " + i)
                remove = True
        if remove:
            pPerm.remove(j)
            remove = False

    # Get number of permissions that are in the manifest but not used in the pDroid permissions
    # The assumption here is that the permissions from pDroid will overlap with those of the manifest
    # We just care about how many more there are in the manifest than in pDroid
    difference = len(app_perm_list) - len(pPerm) 

    os.chdir("..")
    output = apk + ";" + str(app_perm_list) + ";" + str(pPerm) + ";" + str(difference) + "\n"
    out.write(output)

    # Move everything back to where it was
    mvBak = "mv PDroid/" + pDir + " " + apkName + " ."
    os.system(mvBak)

out.close

# NOTES:
# Compile the results into a list with 4 columns, apk name, manifest perms, pdroid perms, # of perms from manifest (not) used
