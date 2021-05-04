class Timeline(object):
  timeline: str = ""

  """Wrapper for Google Timeline."""
  def __init__(self, timeline: str = ""):
    self.timeline = timeline

  def create_timeline_url(self, date: str):
    return self.timeline + date
