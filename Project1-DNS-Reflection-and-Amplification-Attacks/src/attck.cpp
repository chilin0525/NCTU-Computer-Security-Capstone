#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <iomanip>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <netinet/udp.h>
#include <memory.h>
#include <unistd.h>
#include <linux/if_ether.h>
#include <linux/if_packet.h> // sockaddr_ll
#include <arpa/inet.h>
#include <netinet/if_ether.h>

#define BUFF_LEN 100

struct UDP_PSD_Header{
	u_int32_t src;
	u_int32_t des;
	u_int8_t  mbz;
	u_int8_t  ptcl;
	u_int16_t len;
};

// unsigned short csum(unsigned short *buf, int nwords){ 
// 	unsigned long sum;
// 	for (sum = 0; nwords > 0; nwords--){
// 		sum += *buf++;
// 	}
// 	sum = (sum >> 16) + (sum & 0xffff);
// 	sum += (sum >> 16);
// 	return (unsigned short)(~sum);
// }

unsigned short checksum(unsigned short *buff, int _16bitword){
	unsigned long sum;
	for (sum = 0; _16bitword > 0; _16bitword--)
		sum += htons(*(buff)++);
	sum = ((sum >> 16) + (sum & 0xFFFF));
	sum += (sum >> 16);
	return (unsigned short)(~sum);
}

int main(int argc, char *argv[]){

	// unsigned char DNS[] = { 0xd8, 0xcb , 0x01, 0x00, 0x00, 0x01, 0x00 ,0x00,
	// 	0x00, 0x00, 0x00, 0x00, 0x03, 0x77, 0x77, 0x77,
	// 	0x08, 0x63, 0x68, 0x6f, 0x6e, 0x67, 0x66, 0x65,
	// 	0x72, 0x02, 0x63, 0x6e, 0x00, 0x00, 0x01, 0x00,
	// 	0x01 };

	unsigned char DNS[] = { 0xda, 0x72, 0x01, 0x00, 0x00, 0x01,
		0x00,0x00,0x00,0x00,0x00,0x01,0x03,0x77,0x77,0x77,0x06,0x67,0x6f,0x6f,0x67,0x6c,
		0x65,0x03,0x63,0x6f,0x6d,0x00,0x00,0x01,0x00,0x01,0x00,0x00,0x29,0x02,0x00,0x00,
		0x00,0x00,0x00,0x00,0x00
	};

	if (argc != 4){
		// argv must equal to 4
		printf("Invalid parameters\n");
		exit(-1);
	}

	// Create a raw socket with UDP protocol
	int sd = socket(AF_INET, SOCK_RAW, IPPROTO_UDP);
	if (sd < 0){
		perror("create socket filed error\n");
		exit(-1);
	}else{
		printf("create socket successfully\n");
	}

	// create send buffer and init it
	char buffer[BUFF_LEN];
	memset(buffer, 0, BUFF_LEN);

	// construct ip header
	struct iphdr *ip = (struct iphdr *)buffer;

	ip->ihl = 5;
	ip->version = 4; 
	ip->tos = 0;	 
	// ip->tot_len = ((sizeof(struct iphdr) + sizeof(struct udphdr) + sizeof(DNS)));
	ip->id = htons(10201);
	ip->ttl = 64;	   
	ip->protocol = 17; // UDP
	ip->check = 0;
	ip->saddr = inet_addr(argv[1]);
	ip->daddr = inet_addr(argv[3]);

	// construct udp header
	struct udphdr *udp = (struct udphdr *)(buffer + sizeof(struct iphdr));

	udp->source = htons(7);
	udp->dest 	= htons(53);
	// udp->len = htons(sizeof(struct udphdr)+sizeof(DNS));

	// Filling length of IP header and UDP header
	ip->tot_len = htons(sizeof(struct iphdr)  + sizeof(struct udphdr) + sizeof(DNS));
	udp->len 	= htons(sizeof(struct udphdr) + sizeof(DNS));

	printf("ip len : %d\n", ip->tot_len);
	printf("udp len : %d\n",udp->len);

	char * forUDPCheckSum = new char[sizeof(UDP_PSD_Header) + sizeof(udphdr)+sizeof(DNS)+1];
	memset(forUDPCheckSum, 0, sizeof(UDP_PSD_Header) + sizeof(udphdr) + sizeof(DNS) + 1);
	
	UDP_PSD_Header * udp_psd_Header = (UDP_PSD_Header *)forUDPCheckSum;
	
	udp_psd_Header->src  = inet_addr(argv[1]);
	udp_psd_Header->des  = inet_addr(argv[3]);
	udp_psd_Header->mbz  = 0;
	udp_psd_Header->ptcl = 17;
	udp_psd_Header->len  = htons(sizeof(udphdr)+sizeof(DNS));

	// checksom
	memcpy(forUDPCheckSum + sizeof(UDP_PSD_Header)					, udp, sizeof(udphdr));
	memcpy(forUDPCheckSum + sizeof(UDP_PSD_Header) + sizeof(udphdr)	, DNS, sizeof(DNS));

	udp->check = checksum((unsigned short *)forUDPCheckSum, (sizeof(udphdr) + sizeof(UDP_PSD_Header) + sizeof(DNS)+1)/2);

	// copy dns content to buffer
	memcpy(buffer + sizeof(iphdr) + sizeof(udphdr), DNS, sizeof(DNS));

	struct sockaddr_in din;
	din.sin_family 		= AF_INET;
	din.sin_addr.s_addr = inet_addr(argv[3]);
	din.sin_port 		= htons(53);

	for (int i = 1; i <= 3; i++){
		if (sendto(sd, buffer, ip->tot_len, 0, (struct sockaddr *)&din, sizeof(din)) < 0){
			perror("send error\n");
			exit(0);
		}else{
			printf("send success, index:%d\n", i);
			sleep(1);
		}
	}

	close(sd);
	return 0;
}
