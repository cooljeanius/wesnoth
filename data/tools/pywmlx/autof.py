import os
import re


def autoscan(pathdir):
    filelist = []
    parentdir = os.path.realpath(os.path.join(pathdir, ".."))
    for root, dirs, files in os.walk(pathdir, topdown=False):
        for name in files:
            rx = re.compile(r"\.(cfg|lua)$", re.I)
            m = re.search(rx, name)
            if m:
                value = os.path.realpath(os.path.join(root, name))
                value = value[len(parentdir) + 1 :]
                if os.name == "posix":
                    value = re.sub(r"^\/", "", value)
                else:
                    value = re.sub(r"^(?:[A-Za-z]\:)?\\", "", value)
                    # use Unix path separators even on Windows
                    value = value.replace("\\", "/")
                filelist.append(value)
                # end if m
            # end for name
        # end for root
    # end for scandir
    return (parentdir, filelist)


# end autoscan
