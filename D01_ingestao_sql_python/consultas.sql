-- Times que jogara com o Brasil e sua totalidade

SELECT away_team as time, count(*) as jogos_contra_brasil
FROM football.results
WHERE home_team = 'Brazil' OR away_team  = 'Brazil'
GROUP BY away_team
ORDER BY jogos_contra_brasil DESC