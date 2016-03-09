#!/usr/bin/env perl
use Mojo::Weixin;
my ($host,$port,$post_api);

$host = "127.0.0.1"; #发送消息接口监听地址，修改为自己希望监听的地址
$port = 3000;      #发送消息接口监听端口，修改为自己希望监听的端口
#$post_api = 'http://127.0.0.1:3000/post_api';  #接收到的消息上报接口，如果不需要接收消息上报，可以删除或注释此行

my $client = Mojo::Weixin->new(log_level=>"info",ua_debug=>0);
$client->login();
$client->load("ShowMsg");
$client->load("Openwx",data=>{listen=>[{host=>$host,port=>$port}], post_api=>$post_api});
$client->run();