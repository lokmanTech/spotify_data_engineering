import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Tracks
Tracks_node1719629880266 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://my-spotify-de-project/staging/spotify_tracks_data_2023.csv"], "recurse": True}, transformation_ctx="Tracks_node1719629880266")

# Script generated for node Artist
Artist_node1719629869651 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://my-spotify-de-project/staging/spotify_artist_data_2023.csv"], "recurse": True}, transformation_ctx="Artist_node1719629869651")

# Script generated for node Albums
Albums_node1719629878578 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://my-spotify-de-project/staging/spotify-albums_data_2023.csv"], "recurse": True}, transformation_ctx="Albums_node1719629878578")

# Script generated for node Join Artist & Albums
JoinArtistAlbums_node1719665136414 = Join.apply(frame1=Artist_node1719629869651, frame2=Albums_node1719629878578, keys1=["id"], keys2=["artist_id"], transformation_ctx="JoinArtistAlbums_node1719665136414")

# Script generated for node Join with tracks
Joinwithtracks_node1719630685234 = Join.apply(frame1=Tracks_node1719629880266, frame2=JoinArtistAlbums_node1719665136414, keys1=["id"], keys2=["track_id"], transformation_ctx="Joinwithtracks_node1719630685234")

# Script generated for node Drop Fields
DropFields_node1719630853452 = DropFields.apply(frame=Joinwithtracks_node1719630685234, paths=["`.id`", "id"], transformation_ctx="DropFields_node1719630853452")

# Script generated for node Destination
Destination_node1719631338232 = glueContext.write_dynamic_frame.from_options(frame=DropFields_node1719630853452, connection_type="s3", format="glueparquet", connection_options={"path": "s3://my-spotify-de-project/datawarehouse/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="Destination_node1719631338232")

job.commit()