/**
 * Copyright 2020 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef MINDSPORE_LITE_TOOLS_OPTIMIZER_FUSION_LAYER_NORM_FUSION_H_
#define MINDSPORE_LITE_TOOLS_OPTIMIZER_FUSION_LAYER_NORM_FUSION_H_

#include <vector>
#include <memory>
#include <string>
#include "backend/optimizer/common/optimizer.h"
#include "utils/utils.h"

namespace mindspore {
namespace opt {

class LayerNormFusion : public PatternProcessPass {
 public:
  explicit LayerNormFusion(const std::string &name = "layer_norm_fusion", bool multigraph = true)
      : PatternProcessPass(name, multigraph) {
    input_ = std::make_shared<Var>();
    gamma_ = std::make_shared<Var>();
    beta_ = std::make_shared<Var>();
    epsilon_ = std::make_shared<Var>();
  }

  ~LayerNormFusion() override = default;
  const BaseRef DefinePattern() const override;
  const AnfNodePtr Process(const FuncGraphPtr &, const AnfNodePtr &, const EquivPtr &) const override;

 private:
  CNodePtr CreateLayerNormNode(const FuncGraphPtr &func_graph, const EquivPtr &equiv, const std::vector<int> &shape,
                               const float epsilon) const;
  VarPtr input_;
  VarPtr gamma_;
  VarPtr beta_;
  VarPtr epsilon_;
};
}  // namespace opt
}  // namespace mindspore

#endif  // MINDSPORE_LITE_TOOLS_OPTIMIZER_FUSION_LAYER_NORM_FUSION_H_
