close all
clear all

datapath = 'E:\data\simulation\temperature_modulation\temp_mod_somatic';
files = dir(datapath);


idx_warm = [];
burst_warm = [];
fr_warm = [];
idx_cool = [];
burst_cool = [];
fr_cool = [];
edges = [0:5:70];
isi_warm = [];
isi_cool = [];
dist_warm = [];
dist_cool = [];
for i = 1:length(files)
    if contains(files(i).name, 'temp28')
        idx_cool = [idx_cool, i];
        load(fullfile(files(i).folder, files(i).name))
        dist_cool = [dist_cool, P.dist(3)];
        t_spike = spike_times(dt, v);
        isi = diff(t_spike);
        isi_cool = [isi_cool;histcounts(isi, edges)];
        t_burst_idx = find(diff(t_spike)<=20)+1;
        burst_cool = [burst_cool, length(t_burst_idx)/length(t_spike)];
        fr_cool = [fr_cool, length(t_spike)/(double(T)/1000)];
    elseif contains(files(i).name, 'temp34')
        idx_warm = [idx_warm, i];
        load(fullfile(files(i).folder, files(i).name))
        dist_warm = [dist_warm, P.dist(3)];
        t_spike = spike_times(dt, v);
        isi = diff(t_spike);
        isi_warm = [isi_warm;histcounts(isi, edges)];
        t_burst_idx = find(diff(t_spike)<=20)+1;
        burst_warm = [burst_warm, length(t_burst_idx)/length(t_spike)];
        fr_warm = [fr_warm, length(t_spike)/(double(T)/1000)];
    end
end

burst_warm(dist_warm<=21) = [];
fr_warm(dist_warm<=21) = [];
burst_cool(dist_cool<=21) = [];
fr_cool(dist_cool<=21) = [];
isi_cool(dist_cool<=21,:) = [];
isi_warm(dist_warm<=21,:) = [];
% addpath(genpath(fullfile(pwd,'GeneSetAnalysisMatlab')))
% color = 'redbluedark';
% cmap = custom_cmap(color);
cmap = colormap(parula);
boxplot_pairwise([burst_cool', burst_warm'], cmap([1,end],:));
boxplot_pairwise([fr_cool', fr_warm'], cmap([1,end],:))

isi_cool = isi_cool/5;
isi_warm = isi_warm/5;
figure
bar(edges(1:end-1)+(edges(2)-edges(1))/2,mean(isi_cool),'FaceColor','None','EdgeColor', cmap(1,:),'LineWidth',1)
hold on
er = errorbar(edges(1:end-1)+(edges(2)-edges(1))/2,mean(isi_cool),std(isi_cool)/size(isi_cool,1));
er.Color = cmap(1,:);                            
er.LineStyle = 'none';  

figure
bar(edges(1:end-1)+(edges(2)-edges(1))/2,mean(isi_warm),'FaceColor','None','EdgeColor', cmap(end,:),'LineWidth',1)
hold on
er = errorbar(edges(1:end-1)+(edges(2)-edges(1))/2,mean(isi_warm),std(isi_warm)/size(isi_warm,1));
er.Color = cmap(end,:);                            
er.LineStyle = 'none';  