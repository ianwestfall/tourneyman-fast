export default function competitorDisplayFilter(competitor) {
  return competitor.firstName !== null
    ? `${competitor.firstName} ${competitor.lastName}`
    : `${competitor.lastName}`;
}
