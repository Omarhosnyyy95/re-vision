import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script generated for node Category_tree Source
Category_treeSource_node1 = glueContext.create_dynamic_frame.from_catalog(
    database="revision",
    table_name="category_tree",
    transformation_ctx="Category_treeSource_node1",
)

# Script generated for node events Source
eventsSource_node1655055455867 = glueContext.create_dynamic_frame.from_catalog(
    database="revision",
    table_name="events",
    transformation_ctx="eventsSource_node1655055455867",
)

# Script generated for node itemproperties source
itempropertiessource_node1655055688963 = glueContext.create_dynamic_frame.from_catalog(
    database="revision",
    table_name="item_properties",
    transformation_ctx="itempropertiessource_node1655055688963",
)

# Script generated for node ApplyMapping
ApplyMapping_node2 = ApplyMapping.apply(
    frame=Category_treeSource_node1,
    mappings=[
        ("categoryid", "long", "categoryid", "long"),
        ("parentid", "long", "parentid", "long"),
    ],
    transformation_ctx="ApplyMapping_node2",
)

# Script generated for node Apply Mapping
ApplyMapping_node1655055468757 = ApplyMapping.apply(
    frame=eventsSource_node1655055455867,
    mappings=[
        ("timestamp", "long", "timestamp", "long"),
        ("visitorid", "long", "visitorid", "long"),
        ("event", "string", "event", "string"),
        ("itemid", "long", "itemid", "long"),
        ("transactionid", "long", "transactionid", "long"),
    ],
    transformation_ctx="ApplyMapping_node1655055468757",
)

# Script generated for node Apply Mapping
ApplyMapping_node1655055722263 = ApplyMapping.apply(
    frame=itempropertiessource_node1655055688963,
    mappings=[
        ("timestamp", "long", "timestamp", "long"),
        ("itemid", "long", "itemid", "long"),
        ("property", "string", "property", "string"),
        ("value", "string", "value", "string"),
    ],
    transformation_ctx="ApplyMapping_node1655055722263",
)

# Script generated for node S3 bucket
S3bucket_node3 = glueContext.getSink(
    path="s3://revisiontest/outputdata/category_tree/",
    connection_type="s3",
    updateBehavior="LOG",
    partitionKeys=["event"],
    compression="gzip",
    enableUpdateCatalog=True,
    transformation_ctx="S3bucket_node3",
)
S3bucket_node3.setCatalogInfo(
    catalogDatabase="revision", catalogTableName="category_tree_output"
)
S3bucket_node3.setFormat("glueparquet")
S3bucket_node3.writeFrame(ApplyMapping_node2)
# Script generated for node Amazon S3
AmazonS3_node1655055480008 = glueContext.getSink(
    path="s3://revisiontest/outputdata/events/",
    connection_type="s3",
    updateBehavior="LOG",
    partitionKeys=["event", "itemid"],
    compression="gzip",
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1655055480008",
)
AmazonS3_node1655055480008.setCatalogInfo(
    catalogDatabase="revision", catalogTableName="events_output"
)
AmazonS3_node1655055480008.setFormat("glueparquet")
AmazonS3_node1655055480008.writeFrame(ApplyMapping_node1655055468757)
# Script generated for node Amazon S3
AmazonS3_node1655055732372 = glueContext.getSink(
    path="s3://revisiontest/outputdata/item_properties/",
    connection_type="s3",
    updateBehavior="LOG",
    partitionKeys=["itemid", "property"],
    compression="gzip",
    enableUpdateCatalog=True,
    transformation_ctx="AmazonS3_node1655055732372",
)
AmazonS3_node1655055732372.setCatalogInfo(
    catalogDatabase="revision", catalogTableName="item_properties_output"
)
AmazonS3_node1655055732372.setFormat("glueparquet")
AmazonS3_node1655055732372.writeFrame(ApplyMapping_node1655055722263)
job.commit()
