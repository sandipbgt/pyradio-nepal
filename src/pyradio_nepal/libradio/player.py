import subprocess
import os
import logging
import platform

logger = logging.getLogger(__name__)


class Player:
    process = None

    def __init__(self):
        pass

    def __del__(self):
        self.close()

    def isPlaying(self):
        return bool(self.process)

    def play(self, streamUrl):
        self.close()
        opts = self._buildStartOpts(streamUrl)
        self.process = subprocess.Popen(opts, shell=False,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug("Player started")

    def _sendCommand(self, command):
        if(self.process is not None):
            try:
                if logger.isEnabledFor(logging.DEBUG):
                    logger.debug("Command: {}".format(command).strip())
                self.process.stdin.write(command.encode("utf-8"))
            except:
                msg = "Error when sending: {}"
                logger.error(msg.format(command).strip(), exc_info=True)

    def close(self):
        self._stop()

        if self.process is not None:
            os.kill(self.process.pid, 15)
            self.process.wait()
        self.process = None


    def _buildStartOpts(self, streamUrl):
        pass

    def mute(self):
        pass

    def _stop(self):
        pass

    def volumeUp(self):
        pass

    def volumeDown(self):
        pass

class MpPlayer(Player):

    PLAYER_CMD = "mplayer"

    def _buildStartOpts(self, streamUrl):
        return [self.PLAYER_CMD, "-quiet", streamUrl]

    def mute(self):
        self._sendCommand("m")

    def pause(self):
        self._sendCommand("p")

    def _stop(self):
        self._sendCommand("q")

    def volumeUp(self):
        self._sendCommand("*")

    def volumeDown(self):
        self._sendCommand("/")

class VlcPlayer(Player):

    PLAYER_CMD = "/Applications/VLC.app/Contents/MacOS/VLC" if platform.system() == 'Darwin' else "cvlc"

    def _buildStartOpts(self, streamUrl):
        return [self.PLAYER_CMD, "-I", "rc", streamUrl]

    def mute(self):
        if not self.muted:
            self._sendCommand("volume 0\n")
            self.muted = True
        else:
            self._sendCommand("volume 256\n")
            self.muted = False

    def pause(self):
        self._sendCommand("stop\n")

    def _stop(self):
        self._sendCommand("shutdown\n")

    def volumeUp(self):
        self._sendCommand("volup\n")

    def volumeDown(self):
        self._sendCommand("voldown\n")
