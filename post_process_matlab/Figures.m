colors = [[0.0390000000000000,0.345000000000000,0.529000000000000]; [0.573000000000000,0.216000000000000,0.212000000000000]];

%% Figure 5F
load(fullfile(pwd, 'stat', 'Figure5F.mat'))
figure
bar(edges(1:end-1)+(edges(2)-edges(1))/2,mean(isi_cool),'FaceColor','None','EdgeColor', colors(1,:),'LineWidth',1)
hold on
er = errorbar(edges(1:end-1)+(edges(2)-edges(1))/2,mean(isi_cool),std(isi_cool)/size(isi_cool,1));
er.Color = colors(1,:);                            
er.LineStyle = 'none';  
title('with cooling')

figure
bar(edges(1:end-1)+(edges(2)-edges(1))/2,mean(isi_warm),'FaceColor','None','EdgeColor', colors(2,:),'LineWidth',1)
hold on
er = errorbar(edges(1:end-1)+(edges(2)-edges(1))/2,mean(isi_warm),std(isi_warm)/size(isi_warm,1));
er.Color = colors(2,:);                            
er.LineStyle = 'none';  
title('without cooling')

boxplot_pairwise([burst_cool', burst_warm'],colors);
xticks([1,2]), xticklabels({'cooling', 'no cooling'}), ylabel('Burst Prob.')
%% Figure S8D
load(fullfile(pwd, 'stat', 'FigureS8D.mat'))
boxplot_pairwise([burst_cool', burst_warm'],colors);
xticks([1,2]), xticklabels({'cooling', 'no cooling'}), ylabel('Burst Prob.')

boxplot_pairwise([fr_cool', fr_warm'],colors);
xticks([1,2]), xticklabels({'cooling', 'no cooling'}), ylabel('FR [Hz]')
%% Figure S8E
load(fullfile(pwd, 'stat', 'FigureS8E.mat'))
boxplot_pairwise([burst_cool', burst_warm'],colors);
xticks([1,2]), xticklabels({'cooling', 'no cooling'}), ylabel('Burst Prob.')

boxplot_pairwise([fr_cool', fr_warm'],colors);
xticks([1,2]), xticklabels({'cooling', 'no cooling'}), ylabel('FR [Hz]')