/**
 * Converts a tournament status from int to a human readable string.
 * @param {*} value
 * @returns
 */
export default function tournamentStatusFilter(value) {
  return ['Pending', 'Ready to Start', 'Active', 'Complete'][value];
}
