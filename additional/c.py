d={
  "FaceDetails": [
    {
      "BoundingBox": {
        "Height": 0.3194810748100281,
        "Left": 0.40016457438468933,
        "Top": 0.10564027726650238,
        "Width": 0.2342345118522644
      },
      "Confidence": 99.99998474121094,
      "Landmarks": [
        {
          "Type": "eyeLeft",
          "X": 0.5031697750091553,
          "Y": 0.22545810043811798
        },
        {
          "Type": "eyeRight",
          "X": 0.6005402207374573,
          "Y": 0.23324185609817505
        },
        {
          "Type": "mouthLeft",
          "X": 0.511383056640625,
          "Y": 0.34399867057800293
        },
        {
          "Type": "mouthRight",
          "X": 0.5910546779632568,
          "Y": 0.35028594732284546
        },
        {
          "Type": "nose",
          "X": 0.5758214592933655,
          "Y": 0.28490522503852844
        }
      ],
      "Pose": {
        "Pitch": 12.547468185424805,
        "Roll": 4.487471103668213,
        "Yaw": 9.290149688720703
      },
      "Quality": {
        "Brightness": 86.37849426269531,
        "Sharpness": 92.22801208496094
      }
    }
  ],
  "ResponseMetadata": {
    "HTTPHeaders": {
      "connection": "keep-alive",
      "content-length": "678",
      "content-type": "application/x-amz-json-1.1",
      "date": "Tue, 09 Jun 2020 12:10:45 GMT",
      "x-amzn-requestid": "ee90d488-af43-43c9-b5e8-8d844a2321c4"
    },
    "HTTPStatusCode": 200,
    "RequestId": "ee90d488-af43-43c9-b5e8-8d844a2321c4",
    "RetryAttempts": 0
  }
}

print(d['FaceDetails'][0]['Confidence'])