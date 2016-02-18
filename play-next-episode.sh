#!/usr/bin/env bash
cd /home/nazgul/Prog/Home/PlayNextEpisode/

rm vlc.log pid

python play_next_episode.py

sleep 1


# TODO try moving this to python
#tail -fn0 vlc.log | while read line ; do
#        echo "$line" | grep "starting playback of the new playlist item"
#        if [ $? = 0 ]
#        then
#                PID=$(<pid)
#                kill -15 $PID
#                rm vlc.log pid
#                bash play_next_episode.sh
#        fi
#done