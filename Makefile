.PHONY: show
show: recent_plan

.PHONY: recent_plan
recent_plan:
	./visualize.py data/plan_2019-03.csv

.PHONY: git
git:
	git add .
	git commit -m "$(shell date "+%Y-%m-%d")"
	git push origin master
