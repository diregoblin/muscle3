PREFIX ?= /usr/local

# Get source paths
hdrdir := $(CURDIR)/../../src
srcdir := $(CURDIR)/../../src/ymmsl
srcdirs := $(srcdir)
objdir := $(CURDIR)/objs

VPATH := $(srcdir)
source_files := $(foreach dir,$(srcdirs),$(wildcard $(dir)/*.cpp))
objects := $(source_files:$(srcdir)%.cpp=$(objdir)%.o)
lobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.lo)
dobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.do)
dlobjects := $(source_files:$(srcdir)%.cpp=$(objdir)%.dlo)
deps := $(source_files:$(srcdir)%.cpp=$(objdir)%.d)

public_headers := ymmsl/compute_element.hpp ymmsl/identity.hpp ymmsl/model.hpp
public_headers += ymmsl/settings.hpp ymmsl/settings.tpp ymmsl/ymmsl.hpp
installed_headers := $(public_headers:%=$(PREFIX)/include/%)

CXXFLAGS += -Wall -pedantic -std=c++14 -I$(hdrdir)
export CXXFLAGS
DEBUGFLAGS := -g
export DEBUGFLAGS


.PHONY: all
all: libymmsl.a libymmsl.so libymmsl_d.a libymmsl_d.so

.PHONY: tests
tests: libymmsl.a
	$(MAKE) -C tests tests

.PHONY: test
test:
	$(MAKE) -C tests test

.PHONY: clean
clean:
	rm -f libymmsl.a libymmsl.so
	rm -rf objs
	$(MAKE) -C tests clean

.PHONY: distclean
distclean: clean
	$(MAKE) -C tests distclean

.PHONY: install
install: all $(installed_headers)
	@echo
	@echo Installing libymmsl to $(PREFIX)
	@mkdir -p $(PREFIX)/lib
	cp libymmsl.a $(PREFIX)/lib
	cp libymmsl_d.a $(PREFIX)/lib
	cp libymmsl.so $(PREFIX)/lib
	cp libymmsl_d.so $(PREFIX)/lib


cleantargets := clean distclean
ifeq "$(filter $(MAKECMDGOALS),$(cleantargets))" ""

-include $(deps)

endif

$(objdir)/%.d: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -E -MM -MT $(@:.d=.o) $< -o $@

$(objdir)/%.o: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $< -o $@

$(objdir)/%.lo: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -fPIC -c $< -o $@

$(objdir)/%.do: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $(DEBUGFLAGS) -c $< -o $@

$(objdir)/%.dlo: %.cpp
	@mkdir -p $(@D)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $(DEBUGFLAGS) -fPIC -c $< -o $@

libymmsl.a: $(objects)
	ar rcs $@ $^

libymmsl.so: $(lobjects)
	$(CXX) -shared -o $@ $^

libymmsl_d.a: $(dobjects)
	ar rcs $@ $^

libymmsl_d.so: $(dlobjects)
	$(CXX) -shared -o $@ $^

$(PREFIX)/include/%.hpp: $(hdrdir)/%.hpp
	@mkdir -p $(@D)
	cp $< $@

$(PREFIX)/include/%.tpp: $(hdrdir)/%.tpp
	@mkdir -p $(@D)
	cp $< $@

