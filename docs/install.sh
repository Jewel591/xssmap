echo -e ""
echo -e "\033[34m==>  \033[0m\033[1mCloning Repository ... \033[0m"
git clone https://github.com/Jewel591/CheckXSS.git 
if [ "$?"!= "0" ]; then
   echo "[error] git clone failed ..."
   exit 1
cd CheckXSS
echo -e "\033[34m==>  \033[0m\033[1mInstall Python3 module ... \033[0m"
pip3 install -r requirement.txt -i https://pypi.douban.com/simple 
if [ "$?"!= "0" ]; then
   echo "[error] pip3 install failed "
   exit 1
echo "Successful installation, thanks"
