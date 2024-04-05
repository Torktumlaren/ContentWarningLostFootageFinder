import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

TEMP_PATH = os.getenv("TEMP")
RECORDINGS_PATH = os.path.join(TEMP_PATH, "rec")


def findLostDirectories() -> list[str]:
    '''Finds and returns a list of directories that don't have a saved recording.

    '''
    lostDirectories = []
    for recording in os.listdir(RECORDINGS_PATH):
        recording = os.path.join(RECORDINGS_PATH, recording)
        clipsDirectory = os.listdir(recording)

        recordingExists = "fullRecording.webm" in clipsDirectory
        if not recordingExists:
            lostDirectories.append(recording)
            print(f"Lost footage found at \"{recording}\"")
    return lostDirectories


if __name__ == "__main__":
    lostDirectories = findLostDirectories()

    print("Concatenating clips, this may take a few minutes...")
    for index, directory in enumerate(lostDirectories):
        clipFolders = os.listdir(directory)

        # Sort clip folders by creation date to get them in the right order.
        clipFolders.sort(key=lambda folder: os.path.getctime(os.path.join(directory, folder)))

        videoClips = []
        for clipDirectory in clipFolders:
            path = os.path.join(directory, clipDirectory, "output.webm")
            videoClips.append(VideoFileClip(path))

        print(f"Processing footage #{index}...")
        finalClip = concatenate_videoclips(videoClips)
        finalClip.write_videofile(f"FoundFootage{index}.webm")