FROM gliderlabs/alpine:3.4  
MAINTAINER toasterlint "henry@toasterlint.com  
  
RUN apk add \--no-cache nodejs  
  
RUN \  
apk add \--no-cache g++ gcc git make bash python && \  
export MAKEFLAGS=-j8 && \  
npm install -g storjshare-daemon && \  
npm cache clear \--force && \  
apk del \--no-cache g++ gcc git make bash python  
  
ENV USE_HOSTNAME_SUFFIX=FALSE  
ENV DATADIR=/storj  
ENV WALLET_ADDRESS=  
ENV SHARE_SIZE=1TB  
ENV RPCADDRESS=0.0.0.0  
ENV RPCPORT=4000  
EXPOSE 4000/tcp  
  
ADD versions entrypoint /  
ENTRYPOINT ["/entrypoint"]  
  

