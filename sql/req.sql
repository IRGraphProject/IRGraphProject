select w1.word, w2.word, s.sig from words w1, words w2, co_s s
where w1.w_id = s.w1_id and w2.w_id = s.w2_id order by s.sig desc;
