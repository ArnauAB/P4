graph_lp=importdata('lp.txt');
figure(1);
plot(graph_lp(:,1),graph_lp(:,2),'.')
grid on
xlabel('a(2)'),ylabel('a(3)'),title('LP')

graph_lpcc=importdata('lpcc.txt');
figure(2);
plot(graph_lpcc(:,1),graph_lpcc(:,2),'.')
grid on
xlabel('a(2)'),ylabel('a(3)'),title('LPCC')

graph_mfcc=importdata('mfcc.txt');
figure(3);
plot(graph_mfcc(:,1),graph_mfcc(:,2),'.')
grid on
xlabel('a(2)'),ylabel('a(3)'),title('MFCC')

