#ifdef FROM_CMSSW
#include "../interface/Leaf.h"
#else
#include <Leaf.h>
#endif

namespace ROOT {
    Leaf::Leaf(const std::string& name, const TreeWrapperAccessor& tree):
        m_name(name),
        m_tree(tree) {

        }
};
