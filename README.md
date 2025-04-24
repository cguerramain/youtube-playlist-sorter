# youtube-playlist-sorter

Youtube lets you manually sort a playlist with the "Manual" sort setting.
However, when you add a new video to the playlist, it adds it at the bottom
instead of at the top. This is especially annoying for Youtube Music playlists
where I want the most recent addition to be at the top. You can set it to sort
by "Date Added" to get this behavior, but then you can't sort it manually
which is something that's especially useful for a music playlist.

This repo is a workaround to manually sort a playlist and allow new additions
to be added to the top. It works by doing the following:

0) Provide a playlist and a CSV file of manually sorted video names.
1) Get all the videos in the playlist.
2) Store the videos in a temporary CSV.
3) Remove all the videos from the playlist.
5) Set the playlist to sort by "Date Added"
6) Re-add the videos in the sorted order.

Now the videos will be in the manually sorted order and any new videos will be
added at the top of the playlist.
