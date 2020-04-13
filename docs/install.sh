echo "repository name: CheckXSS by Jewel591"
git clone https://github.com/Jewel591/CheckXSS.git 
if [ "$?"!= "0" ]; then
   echo "[error] git clone failed ..."
   exit 1
cd CheckXSS
pip3 install -r requirement.txt -i https://pypi.douban.com/simple 
if [ "$?"!= "0" ]; then
   echo "[error] pip3 install failed "
   exit 1
echo "Successful installation, thanks"
