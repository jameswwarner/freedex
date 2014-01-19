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

--- freedex500 (slim)
select s.id, s.ticker, (s.num_shares * q.close_price) as mktcap FROM stock s join stock_quote q on q.stock_id = s.id  where (s.num_shares * q.close_price) >4000000000 and (252 * q.volume /s.num_shares) >= 1.0 and (q.volume*252/12.0) > 250000 order by mktcap desc limit 500;

--- sp500 reference
select s.id, s.ticker, (s.num_shares * q.close_price) as mktcap FROM stock s join stock_quote q on q.stock_id = s.id join sp500ref r on s.ticker = r.ticker;

--- fixups needed for ALLE, BRK.B, BF.B, GHC
update stock set num_shares=1650000 where ticker="BRK.B";
update stock set num_shares=213200000 where ticker="BF.B";
update stock set num_shares=96030000 where ticker="ALLE";
update stock set num_shares=7420000 where ticker="GHC";

-- explore metrics
select s.ticker, s.name, se.name sector_name, indu.name industry_name, q.close_price, (s.num_shares * q.close_price) as mktcap, (252 * q.volume /s.num_shares) AS tradeRatio, (252 * q.volume /s.num_shares) >= 1.0 and (q.volume*252/12.0) AS monthlyVol FROM stock s join stock_quote q on q.stock_id = s.id join sector se on s.sector_id = se.id join industry indu on s.industry_id = indu.id where (s.num_shares * q.close_price) >4000000000 and (252 * q.volume /s.num_shares) >= 1.0 and (q.volume*252/12.0) > 250000 order by mktcap desc limit 500;


insert into tmp_r2 (id,ticker,mktcap) select s.id, s.ticker, (s.num_shares * q.close_price) as mktcap FROM stock s join stock_quote q on q.stock_id = s.id  where (s.num_shares * q.close_price) >4000000000 and (252 * q.volume /s.num_shares) >= 1.0 and (q.volume*252/12.0) > 250000 order by mktcap desc limit 500;

select sum(mktcap) from tmp_r2;
update tmp_r2 set sum_mktcap=13293652450966.598;

 insert into index_component (version,index_snapshot_id, stock_id, weight) select 0,1,id AS stock_id, weight from tmp_r2;
