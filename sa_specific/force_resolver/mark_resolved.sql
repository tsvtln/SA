UPDATE transactions SET conflicted_elsewhere='N' WHERE conflicted_elsewhere='Y';
UPDATE transaction_conflicts SET resolved='Y' WHERE resolved='N';
UPDATE transaction_logs SET conflicting = 'N' WHERE conflicting = 'Y';
COMMIT;
