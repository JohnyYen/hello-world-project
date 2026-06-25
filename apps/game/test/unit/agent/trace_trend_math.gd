# trace_trend_math.gd
# Manual trace of the trend calculation math to verify behavior
# This is NOT a test - just math verification

# Simulate declining scores
var scores := [0.9, 0.7, 0.5, 0.3, 0.2]

# Calculate blended_score (short term avg for simplicity)
var blended_score := 0.0
for s in scores:
	blended_score += s
blended_score /= scores.size()
print("Blended score (avg): %.4f" % blended_score)

# Calculate WEIGHTED trend
# recent_avg = avg of last 2 = (0.3 + 0.2) / 2 = 0.25
# old_avg = avg of first 2 = (0.9 + 0.7) / 2 = 0.8
# trend = recent_avg - old_avg = 0.25 - 0.8 = -0.55
var recent_avg := (scores[scores.size() - 1] + scores[scores.size() - 2]) / 2.0
var old_avg := (scores[0] + scores[1]) / 2.0
var trend := recent_avg - old_avg
print("Trend (WEIGHTED mode): %.4f" % trend)

# Calculate hybrid metric
var normalized_trend := clamp((trend + 1.0) / 2.0, 0.0, 1.0)
print("Normalized trend: %.4f (from trend %.4f)" % [normalized_trend, trend])

var hybrid := blended_score * 0.7 + normalized_trend * 0.3
print("Hybrid metric: %.4f (%.4f * 0.7 + %.4f * 0.3)" % [hybrid, blended_score, normalized_trend])

# Determine action
var action: String
if hybrid < 0.3:
	action = "decrease_major"
elif hybrid < 0.5:
	action = "decrease_minor"
elif hybrid <= 0.8:
	action = "keep"
elif hybrid <= 0.9:
	action = "increase_minor"
else:
	action = "increase_major"

print("Action: %s (hybrid = %.4f)" % [action, hybrid])
print("")
print("RESULT: For declining scores [0.9, 0.7, 0.5, 0.3, 0.2]")
print("  - Trend is NEGATIVE: %.4f" % trend)
print("  - Hybrid is LOW: %.4f" % hybrid)
print("  - Action triggers DECREASE: %s" % action)