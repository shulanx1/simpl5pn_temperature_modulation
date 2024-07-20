
function t_spike = spike_times(dt, v)
    thresh_cross = find(v(1, :) > 0);
    if length(thresh_cross) > 0
        spikes = find(diff(thresh_cross) > 1) + 1;
        spikes = [1,spikes];
        spikes = thresh_cross(spikes);
        spikes_temp = spikes;
        for k = 1:length(spikes)
            spike = spikes(k);
            spike_w_temp = v(1, spike:min(spike + floor(2/dt), size(v,2)));
            [~,a] = max(spike_w_temp);
            spikes_temp(k) = spike + a;
        end
        t_spike = spikes_temp*dt;
    else
        t_spike = np.array([]);
    end
end