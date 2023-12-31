from sqlalchemy import Boolean, Column, Integer, String
from database import Base

class Projects(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(String,index=True)
    project = Column(String, index=True)
    videoURL = Column(String, index=True)
    needTranscoding = Column(Boolean, default=False)
    needSubtitles = Column(Boolean, default=False)
    needThumbnails = Column(Boolean, default=False)
    transcodingURL = Column(String,default="")
    subtitlesURL = Column(String, default="")
    thumbnailsURL = Column(String, default="")
    createdAt = Column(String, default="")
    modifiedAt = Column(String, default="")