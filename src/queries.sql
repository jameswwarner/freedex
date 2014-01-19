--- S&P500
-- mktcap > 4 billion
select s.ticker, q.close_price, (s.num_shares * q.close_price) as mktcap FROM stock s join stock_quote q on q.stock_id = s.id where (s.num_shares * q.close_price) >4000000000 limit 500;
-- mktcap > 4 billion and annual dollar value traded to adjusted cap > 1.0
-- num trading days in a year is 252.
-- 
select s.ticker, q.close_price, (s.num_shares * q.close_price) as mktcap FROM stock s join stock_quote q on q.stock_id = s.id where (s.num_shares * q.close_price) >4000000000 and (252 * q.volume /s.num_shares) >= 1.0 limit 500;


-- mktcap > 4 billion 
-- and annual dollar value traded to adjusted cap > 1.0
-- and min monthly trading volume of 250k in last 6 months of trading
-- 
--    num trading days in a year is 252.
-- num days in a month = 252/12.0

select s.ticker, s.name, se.name sector_name, indu.name industry_name, q.close_price, (s.num_shares * q.close_price) as mktcap FROM stock s join stock_quote q on q.stock_id = s.id join sector se on s.sector_id = se.id join industry indu on s.industry_id = indu.id where (s.num_shares * q.close_price) >4000000000 and (252 * q.volume /s.num_shares) >= 1.0 and (q.volume*252/12.0) > 250000 order by mktcap desc limit 500;


--- index_definition
select s.id, s.ticker, (s.num_shares * q.close_price) as mktcap FROM stock s join stock_quote q on q.stock_id = s.id join sector se on s.sector_id = se.id join industry indu on s.industry_id = indu.id where (s.num_shares * q.close_price) >4000000000 and (252 * q.volume /s.num_shares) >= 1.0 and (q.volume*252/12.0) > 250000 order by mktcap desc limit 500;

