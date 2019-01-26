.PHONY: show
show: recent_plan

.PHONY: recent_plan
recent_plan:
	./plan_2019-03.py

.PHONY: git
git:
	git add .
	git commit -m "$(shell date "+%Y-%m-%d")"
	git push origin master
