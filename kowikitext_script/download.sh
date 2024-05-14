DATE=$1

wget https://dumps.wikimedia.org/kowiki/${DATE}/kowiki-${DATE}-pages-articles-multistream.xml.bz2
wget https://dumps.wikimedia.org/kowiki/${DATE}/kowiki-${DATE}-pages-articles-multistream-index.txt.bz2

bzip2 -vd kowiki-${DATE}-pages-articles-multistream-index.txt.bz2
bzip2 -vd kowiki-${DATE}-pages-articles-multistream.xml.bz2