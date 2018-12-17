

class ParseTracks:

    def __init__(self, track):
        self.track = track

    def __repr__(self):
        if len(self.track) > 1 :
            self.track.insert(-1, 'and')
            self.track = ', '.join(self.track[:-2]) + ' ' + ' '.join(self.track[-2:])
        else:
            self.track = str(self.track[0])
        return self.track
