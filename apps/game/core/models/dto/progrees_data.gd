## Data Transfer Object for Progress data
class_name ProgressData

## The unique ID of the progress record
var progress_id: int = -1

## The user ID associated with the progress
var user_id

## The segment ID associated with the progress
var segment_id : int

## Number of attempts made for this segment
var attemptat : int

## Time taken to complete the segment in seconds
var time_in_complete : float

## Whether the segment was completed (true/false)
var complete : bool

## Timestamp of the last attempt
var last_try

## Constructor for ProgressData
## @param p_user_id: The user ID associated with the progress
## @param p_segment_id: The segment ID associated with the progress
## @param p_attemptat: Number of attempts made for this segment
## @param p_time_in_complete: Time taken to complete the segment in seconds
## @param p_complete: Whether the segment was completed (true/false)
## @param p_last_try: Timestamp of the last attempt
func _init(p_user_id=null, p_segment_id: int = -1, p_attemptat: int = 0, p_time_in_complete: float = 0.0, p_complete: bool = false, p_last_try=null) -> void:
	user_id = p_user_id
	segment_id = p_segment_id
	attemptat = p_attemptat
	time_in_complete = p_time_in_complete
	complete = p_complete
	last_try = p_last_try