#!/bin/bash
echo -e "\n\033[34m==>  \033[0m\033[1mCloning Repository ... \033[0m"
git clone https://github.com/Jewel591/CheckXSS.git -v
if [ "$?" != "0" ]; then
   echo "Error: git clone failed ..."
   exit 1
fi
cd CheckXSS
echo -e "\n\033[34m==>  \033[0m\033[1mInstall Python3 module ... \033[0m"
pip3 install -r requirements.txt
if [ "$?" != "0" ]; then
   echo "error: pip3 install failed "
   exit 1
fi
echo -e "\n\033[34m==>  \033[0m\033[1mSuccessful installation, thanks \033[0m"
