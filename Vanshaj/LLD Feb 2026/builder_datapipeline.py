from typing import Optional, List

class DataPipeline:
    def __init__(self, 
                    source:str, 
                    destination:str,
                    schedule:str,
                    cleaning_steps:Optional[List[str]] = None, 
                    transformation_steps:Optional[List[str]]=None):
        self.source = source
        self.destination = destination
        self.schedule = schedule
        self.cleaning_steps = cleaning_steps
        self.transformation_steps = transformation_steps
    
    def __str__(self):
        return (
            f"source:{self.source}, destination:{self.destination}, schedule:{self.schedule}, cleaning_steps:{self.cleaning_steps}, transformation_steps:{self.transformation_steps}"
        )

class DataPipelineBuilder:
    def __init__(self):
        self._source = None
        self._destination = None
        self._schedule = None
        self._cleaning_steps = []
        self._transformation_steps = []

    def set_source(self, source:str):
        self._source = source
        return self

    def set_destination(self, destination:str):
        self._destination = destination
        return self

    def add_cleaning_step(self, step):
        self._cleaning_steps.append(step)
        return self

    def add_transformation_step(self, step):
        self._transformation_steps.append(step)
        return self

    def set_schedule(self, schedule):
        self._schedule = schedule
        return self

    def build(self):
        if not self._source:
            raise ValueError("source is required")
        if not self._destination:
            raise ValueError("destination is required")
        if not self._schedule:
            raise ValueError("schedule is required")
        return DataPipeline(
            source=self._source,
            destination=self._destination,
            schedule=self._schedule,
            cleaning_steps=self._cleaning_steps if self._cleaning_steps else None,
            transformation_steps=self._transformation_steps if self._transformation_steps else None
        )


if __name__=="__main__":
    csv_to_s3_pipeline = (
        DataPipelineBuilder()
        .set_source("CSV")
        .set_destination("S3")
        .set_schedule("daily")
        .build()
    )

    print(csv_to_s3_pipeline)

    complex_pipeline = (
        DataPipelineBuilder()
        .set_source("Postgres")
        .add_cleaning_step("remove_nulls")
        .add_cleaning_step("deduplicate")
        .add_transformation_step("aggregate")
        .add_transformation_step("join")
        .set_destination("BigQuery")
        .set_schedule("hourly")
        .build()
    )

    print(complex_pipeline)
